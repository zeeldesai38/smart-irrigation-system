
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort
import pandas as pd

BASE_DIR = Path(__file__).parent

MODEL_PATH = BASE_DIR / "best_gboost_model.onnx"
METADATA_PATH = BASE_DIR / "model_metadata.json"

with open(METADATA_PATH, "r") as file:
    metadata = json.load(file)

FEATURE_COLUMNS = metadata["feature_columns"]
CLASSES = metadata["classes"]

session = ort.InferenceSession(
    str(MODEL_PATH),
    providers=["CPUExecutionProvider"]
)

INPUT_NAME = session.get_inputs()[0].name


def predict_irrigation(input_data):
    """
    input_data: dictionary containing the original 19 input features.
    Returns: High, Low, or Medium.
    """

    input_df = pd.DataFrame([input_data])

    # Use the same one-hot encoding as model training
    input_df = pd.get_dummies(
        input_df,
        columns=input_df.select_dtypes(
            include=["object", "category"]
        ).columns,
        drop_first=False,
        dtype=int
    )

    # Match all 43 training features and their exact order
    input_df = input_df.reindex(
        columns=FEATURE_COLUMNS,
        fill_value=0
    )

    input_array = input_df.to_numpy(dtype=np.float32)

    outputs = session.run(None, {INPUT_NAME: input_array})

    # ONNX output_label contains the predicted class
    predicted_value = outputs[0][0]

    if isinstance(predicted_value, (int, np.integer)):
        return CLASSES[int(predicted_value)]

    return str(predicted_value)
