import os

for i in range(1, 49):
    fs = 'model (' + str(i) + ').PNG'
    ft = '../../../../%02d/model.png' %(i)
    os.rename(fs, ft)
    
