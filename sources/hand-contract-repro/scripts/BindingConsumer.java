import org.example.hand.HandModel;
public final class BindingConsumer {
  public static int inspect(HandModel.Outputs out) {
    return out.getHandednessAsCategoryList().size()
        + out.getLandmarksAsTensorBuffer().getFloatArray().length;
  }
}
