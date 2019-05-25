import os

for i in range(1, 49):
    fs = 'generated/model_1d_' + str(i) + '.png'
    ft = '../../%02d/model.png' %(i)
    os.rename(fs, ft)
    
for i in range(1, 49):
    fs = 'generated/model_1d_' + str(i) + '_s.png'
    ft = '../../%02d/model_s.png' %(i)
    os.rename(fs, ft)
    
