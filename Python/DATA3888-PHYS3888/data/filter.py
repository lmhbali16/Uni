import numpy
import serial

def filter(total_time):

    Fs=20000
    data_total = numpy.array([])
    windowtime = 0.12
    nwin = int(total_time/windowtime)
    window = int(windowtime*Fs)
    window16th = int(window/4)
    def fourierFilter(data, Fs, hpass, lpass):
        L=len(data)/Fs
        Nq=Fs/2
        ff= numpy.arange(-Nq, Nq-1/L, 1/L)
        values = numpy.array(abs(ff))
        searchval = lpass
        index_filter = numpy.where(values > searchval)[0]
        values = numpy.array(abs(ff))
        searchval = hpass
        index_filter2 = numpy.where(values < searchval)[0]
        index_filter = [index_filter,index_filter2]
        F1=numpy.fft.fft(data)
        F=numpy.fft.fftshift(F1)
        for n in index_filter:
            F[n] = 0
        data_filtered = numpy.fft.ifft(numpy.fft.ifftshift(F))
        return data_filtered
    
    
    def read_arduino(ser,inputBufferSize):
        data = ser.read(inputBufferSize)
        out =[(int(data[i])) for i in range(0,len(data))]
        return out
    def process_data(data):
        data_in = numpy.array(data)
        result = []
        i = 1
        while i < len(data_in)-1:
            if data_in[i] > 127:
                # Found beginning of frame
                # Extract one sample from 2 bytes
                intout = (numpy.bitwise_and(data_in[i],127))*128
                i = i + 1
                intout = intout + data_in[i]
                result = numpy.append(result,intout)
            i=i+1
        return result

    try:
        s =serial.Serial(port = 'COM12', baudrate=230400, bytesize=8, stopbits=serial.STOPBITS_ONE)
    except serial.SerialException:
        serial.Serial(port = 'COM12', baudrate=230400, bytesize=8, stopbits=serial.STOPBITS_ONE).close()
        s =serial.Serial(port = 'COM12', baudrate=230400, bytesize=8, stopbits=serial.STOPBITS_ONE)

    data_filtered=[]
    for n in range(1,nwin): 
        data_filtered=[];
        if n == 1:
            olddata=numpy.array(read_arduino(s, window))
            olddata = process_data(olddata.transpose())
            olddatacut=olddata[-(window16th):-1]
            newdata=numpy.array(read_arduino(s, window))
            newdata = process_data(newdata.transpose())
            futuredata=numpy.array(read_arduino(s, window))
            futuredata = process_data(futuredata.transpose())
            futuredatacut = futuredata[0:window16th]
            data1=numpy.concatenate((olddatacut, newdata, futuredatacut))
            data_temp = fourierFilter(data1,Fs/2,0,7)
            data_filtered=data_temp[window16th+1:-window16th]
            baseline=numpy.mean(data_filtered)
        elif n ==nwin:
            olddata=newdata
            newdata = futuredata
            data1=[olddata[-(window16th-1):-1], newdata]
            data_temp= fourierFilter(data1,Fs/2,0,7)
            data_filtered=data_temp[window16th+1:-1]
        else:
            olddata=newdata
            olddatacut=olddata[-(window16th):-1]
            newdata = futuredata
            futuredata=numpy.array(read_arduino(s, window))
            futuredata = process_data(futuredata.transpose())
            futuredatacut = futuredata[0:window16th]
            data1=numpy.concatenate((olddatacut, newdata, futuredatacut))
            data_temp= fourierFilter(data1,Fs/2,0,7)
            data_filtered=data_temp[window16th+1:-window16th]    
        data_filtered = data_filtered-baseline
        data_filtered = data_filtered/400

        data_total = numpy.concatenate((data_total, data_filtered))


    s.flushInput()
    s.flushOutput()
    s.close()
    return data_total
