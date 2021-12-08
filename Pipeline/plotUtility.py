import matplotlib.pyplot as plt

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
from sklearn.metrics import RocCurveDisplay,classification_report,ConfusionMatrixDisplay
def showConfusionMatrix(y_test, y_pred):
    # ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax = ax1)
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
    plt.show()

# TODO : Adapt this to be able to multiclass, very annoying
def showROCCurve(y_test, y_pred):
    # RocCurveDisplay.from_predictions(y_test, y_pred, ax = ax2)
    RocCurveDisplay.from_predictions(y_test, y_pred)