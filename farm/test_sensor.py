import time
import farm

def test_sensor():
    s = farm.RandomSensor('test')
    ret = s.read()
    assert len(ret) == 3

def test_sensor_array():
    array = farm.SensorArray()
    array.append(farm.RandomSensor('test'))
    array.append(farm.RandomSensor('foo'))
    ret = array.read()
    assert len(ret) == 2
    assert len(ret[0]) == 3
    assert len(ret[1]) == 3

def test_dummy_sensor():
    s = farm.RandomSensor('foo', 3)
    ret = s.read()
    assert len(ret) == 3
    assert s.publish() == False

def test_sensor_publish():
    # s = farm.RandomSensor('test', 4)
    # ret = s.read()
    # assert len(ret) == 4
    # assert s.publish()

    s = farm.RandomSensor('test', 3, [1, 2, 4])
    ret = s.read()
    assert len(ret) == 3
    assert s.publish(True)
    data = s.fetch()
    assert ret == data