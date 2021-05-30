import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
from numpy.core.function_base import linspace
from scipy import signal  # 삼각파를 만들때에 사용
import time, sys

# sys.argv를 사용시 추가로 명령어 입력시 입력한 값들을 사용가능
# python 파일이름.py A B C D의 경우 sys.argv는 [파일이름.py, A, B, C, D] 이다.
#print('Command: ', sys.argv, len(sys.argv))

# Setting ----------------------------------------#
fs    = 48000 #[sample/sec]: sampling frequency
type  = sys.argv[1] # 파형 종류
amp   = float(sys.argv[2]) # 진폭
Hertz = float(sys.argv[3]) # 주파수
sec   = float(sys.argv[4]) # 지속시간 [sec]
duty  = 0.5                # duty ratio
if len(sys.argv) == 6 : 
    duty = float(sys.argv[5])
    assert (0<= duty and duty <= 1), 'duty should be 0~1'

# 1. 파형 생성 -------------------------------------#
period_sample = sec*fs; # [sec] * [sample/sec] = [sample]
smp = np.arange(period_sample) # 0~period_sample-1의 array를 반환
tt = smp / fs; # 시간축 vector를 생성
print('주기:',fs/Hertz)
if type == "sin":
    y = amp * np.sin(2*np.pi*Hertz*tt)
    
elif type == "sq":
    y = np.zeros(len(tt)) # 비어있는 vector y를 생성
    for i in range(len(tt)):
        cur_pos = i % (fs/Hertz) # % : 나머지 연산자
        if cur_pos < fs/Hertz * duty : y[i] =  amp
        else :                         y[i] = -amp

elif type == "tr":
    smp = linspace(0, int(period_sample), int(period_sample))  # 0~period_sample-1 까지의 array를 반환
    y = signal.sawtooth(2*np.pi*Hertz*sec*smp, duty)  # [Hertz*sec] = [fs*sec] / [fs/Hertz]


# 2. Outputs ----------------------------------------#
# 2-1. time-domain
print('y:',np.shape(y), np.min(y), np.max(y))
if type == 'sin' or type == 'sq':
    plt.plot(y); plt.show()
elif type == 'tr':
    plt.plot(smp, y); plt.show()

# 2-2. 재생
sd.play(y,fs)
time.sleep(len(y)/fs)

# 2-3. FFT
fft_y = np.abs(np.fft.fft( np.hanning(len(y))*y ))
fft_y = fft_y[:int(len(fft_y)/2)+1]
fbins = np.arange(len(fft_y))
fbins = fbins * (fs/2 / len(fft_y)) # fft의 x축(freq)
plt.plot(fbins, fft_y); plt.show()

