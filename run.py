from pmill import Pmill

pm = Pmill()
pm.executeNotebook()
res = pm.getOutput()
print(res)