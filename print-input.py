class DummyDataReader(CalibrationDataReader):
    def __init__(self):
        self.data_iter = iter([
            {"input.1": np.random.rand(1, 3, 416, 416).astype(np.float32)}
            for _ in range(100)
        ])
