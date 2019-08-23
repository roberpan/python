import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

error=np.random.randn(10)
y=pd.Series(np.sin(np.arange(10)))
y.plot(yerr=error)
plt.show()