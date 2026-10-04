#!/usr/bin/env python3
"""Preserve bounded official source snapshots for P2 mechanism review, not execution."""
import datetime, hashlib, json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
REPO = "https://api.github.com/repos/tensorflow/tflite-support"
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "metadata-contract-mechanism-audit"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()
def digest(b):
    return hashlib.sha256(b).hexdigest()

def main():
    sources = ROOT / "sources"
    sources.mkdir(parents=True, exist_ok=True)
    ref_url = REPO + "/commits/v0.4.4"
    ref_bytes = fetch(ref_url)
    (sources / "commit-v0.4.4.json").write_bytes(ref_bytes)
    commit = json.loads(ref_bytes)["sha"]
    tree_url = REPO + f"/git/trees/{commit}?recursive=1"
    tree_bytes = fetch(tree_url)
    (sources / "tree-v0.4.4.json").write_bytes(tree_bytes)
    tree = json.loads(tree_bytes)
    wanted = []
    for item in tree["tree"]:
        p = item["path"]
        if p.endswith("ImageClassifier.java") or p.endswith("image_classifier_jni.cc"):
            wanted.append(p)
    wanted.extend([
        "tensorflow_lite_support/cc/task/vision/image_classifier.cc",
        "tensorflow_lite_support/cc/task/vision/utils/score_calibration.cc",
        "tensorflow_lite_support/cc/task/core/task_utils.cc",
        "tensorflow_lite_support/cc/task/vision/utils/label_map_utils.cc",
        "tensorflow_lite_support/cc/task/vision/core/classification_head.cc",
        "tensorflow_lite_support/cc/task/processor/classification_postprocessor.cc",
        "tensorflow_lite_support/metadata/cc/metadata_extractor.cc",
        "tensorflow_lite_support/java/src/java/org/tensorflow/lite/support/label/TensorLabel.java",
        "tensorflow_lite_support/java/src/java/org/tensorflow/lite/task/core/TaskJniUtils.java",
        "tensorflow_lite_support/cc/utils/jni_utils.cc",
        "tensorflow_lite_support/cc/task/vision/core/label_map_item.cc",
    ])
    paths = {i["path"] for i in tree["tree"]}
    records = []
    for p in wanted:
        if p not in paths:
            records.append({"repository_path":p,"status":"ABSENT_IN_TAG_TREE"})
            continue
        url = f"https://raw.githubusercontent.com/tensorflow/tflite-support/{commit}/{p}"
        dest = sources / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            data = fetch(url)
            dest.write_bytes(data)
            records.append({"repository_path":p,"url":url,"path":str(dest),"sha256":digest(data),"bytes":len(data),"status":"PRESERVED"})
        except Exception as e:
            records.append({"repository_path":p,"url":url,"status":"ERROR","error":repr(e)})
    result = {"collected_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "tag":"v0.4.4","resolved_commit":commit,
              "reference":{"url":ref_url,"path":str(sources/"commit-v0.4.4.json"),"sha256":digest(ref_bytes)},
              "tree":{"url":tree_url,"path":str(sources/"tree-v0.4.4.json"),"sha256":digest(tree_bytes)},
              "records":records,
              "boundary":"Pinned source explains mechanisms; native binary-source equivalence is not established by Maven version alone."}
    (ROOT/"source-provenance.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"commit":commit,"records":len(records),"status_counts":{s:sum(x["status"]==s for x in records) for s in {x["status"] for x in records}}}))

if __name__ == "__main__":
    main()
