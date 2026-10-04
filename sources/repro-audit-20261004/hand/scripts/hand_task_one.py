import dataclasses, hashlib, json, math, pathlib, struct, sys, traceback
import mediapipe as mp
bundle,image_path,dest=map(pathlib.Path,sys.argv[1:4]);dest.mkdir(parents=True,exist_ok=True)
report={'mediapipe_version':mp.__version__,'bundle_sha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(image_path.read_bytes()).hexdigest(),'initialization_status':'NOT_REACHED','input_preparation_status':'NOT_REACHED','detect_status':'NOT_REACHED'}
stage='task_initialization'
try:
    options=mp.tasks.vision.HandLandmarkerOptions(base_options=mp.tasks.BaseOptions(model_asset_path=str(bundle),delegate=mp.tasks.BaseOptions.Delegate.CPU),running_mode=mp.tasks.vision.RunningMode.IMAGE,num_hands=1,min_hand_detection_confidence=0.5,min_hand_presence_confidence=0.5,min_tracking_confidence=0.5)
    with mp.tasks.vision.HandLandmarker.create_from_options(options) as detector:
        report['initialization_status']='PASS';stage='image_preparation';image=mp.Image.create_from_file(str(image_path));report.update(input_preparation_status='PASS',image_width=image.width,image_height=image.height)
        stage='detect_combined_task';result=detector.detect(image);decoded=dataclasses.asdict(result)
        (dest/'decoded.json').write_text(json.dumps(decoded,indent=2));bits=[]
        def visit(x):
            if isinstance(x,float):
                if not math.isfinite(x):raise ValueError('Nonfinite decoded output')
                bits.append(struct.pack('<f',x))
            elif isinstance(x,list):
                for y in x:visit(y)
            elif isinstance(x,dict):
                for key in sorted(x):visit(x[key])
        visit(decoded);blob=b''.join(bits);(dest/'decoded-float-bits.bin').write_bytes(blob)
        report.update(detect_status='PASS',detected_hands=len(result.hand_landmarks),landmarks_per_hand=[len(h) for h in result.hand_landmarks],world_landmarks_per_hand=[len(h) for h in result.hand_world_landmarks],
          handedness=decoded['handedness'],decoded_sha256=hashlib.sha256(json.dumps(decoded,sort_keys=True,separators=(',',':')).encode()).hexdigest(),decoded_float_bits_sha256=hashlib.sha256(blob).hexdigest(),
          path_exercised='HAND_LANDMARKS_RETURNED' if result.hand_landmarks else 'NO_HAND_PATH_EXERCISED')
except Exception as exc:report.update(earliest_failing_stage=stage,exception_type=type(exc).__name__,exception_message=str(exc),stack_trace=traceback.format_exc())
(dest/'result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
