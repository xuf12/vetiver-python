import pytest
import sklearn
import pydantic
import pandas as pd

from vetiver import mock, VetiverModel, VetiverHandler


class CustomHandler(VetiverHandler):
    def __init__(self, model, ptype_data):
        super().__init__(model, ptype_data)

    def handler_predict(self, input_data, check_ptype):
        if check_ptype == True:
            if isinstance(input_data, pd.DataFrame):
                prediction = self.model.predict(input_data)
            else:
               prediction = self.model.predict([input_data])
        else:
            if not isinstance(input_data, list):
                input_data = [input_data.split(",")]  # user delimiter ?
            prediction = self.model.predict(input_data)

        return prediction


def test_custom_vetiver_model():
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    custom_handler = CustomHandler(model, X)

    v = VetiverModel(
        model=custom_handler,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )

    assert v.description == "A regression model for testing purposes"
    assert isinstance(v.model, sklearn.dummy.DummyRegressor)
    assert isinstance(v.ptype.construct(), pydantic.BaseModel)


def test_custom_vetiver_model():
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    custom_handler = CustomHandler(model, None)

    v = VetiverModel(
        model=custom_handler,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )

    assert v.description == "A regression model for testing purposes"
    assert isinstance(v.model, sklearn.dummy.DummyRegressor)
    assert isinstance(v.ptype.construct(), pydantic.BaseModel)