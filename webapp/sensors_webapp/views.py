from asyncio.format_helpers import extract_stack
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Sensor, SensorReading
from django.core.paginator import Paginator 

# Create your views here.

def home_page(request):
    return render(request,'SensorsDataAPI/home_page.html')

def manage_sensors(request):
    sensors = Sensor.objects.all().order_by('sensor_id')
    if request.POST:
        if "Add" in request.POST:
            add_sensor(request)
        if "Delete" in request.POST:
            delete_sensor(request)
    paginator = Paginator(sensors, 10) 
    page_number = request.GET.get('page')
    sensors = paginator.get_page(page_number)
    dict = {
        'sensors': sensors, 
        'paginator': paginator,
        'page_number': page_number
    }
    return render(request,'SensorsDataAPI/manage_sensors.html', dict)

def manage_readings(request):
    readings = SensorReading.objects.all().order_by('reading_date','reading_time').order_by("-id")
    if request.POST:
        if "Add" in request.POST:
            add_reading(request)
        if "Delete" in request.POST:
            delete_reading(request)
    paginator = Paginator(readings, 10) 
    page_number = request.GET.get('page')
    readings = paginator.get_page(page_number)
    sensors = Sensor.objects.all().order_by('sensor_id')
    dict = {
        'readings': readings, 
        'sensors': sensors,
        'paginator': paginator,
        'page_number': page_number
    }
    return render(request,'SensorsDataAPI/manage_readings.html', dict)

def query_readings(request):
    sensor_types = Sensor.objects.order_by().values_list('type',flat = True).distinct()
    locations = Sensor.objects.order_by().values_list('location',flat = True).distinct()
    times = times_of_day(60)
    readings = SensorReading.objects.all().order_by('reading_date','reading_time')
    filter_values = {
        'sensor_type': "All types",
        'location': "All locations",
        'first_time': "00:00",
        'second_time': "00:00",
    }
    extra_info = {}
    if request.POST:
        filter_values = get_filter_values(request)
        readings = get_readings_filtered(filter_values)
        if len(readings) != 0:
            extra_info = get_extra_info(readings)
    paginator = Paginator(readings, 10) 
    page_number = request.GET.get('page')
    readings = paginator.get_page(page_number)
    dict = {
        'readings': readings, 
        'sensor_types': sensor_types,
        'locations': locations,
        'times': times,
        'paginator': paginator,
    }
    dict.update(filter_values)
    dict.update(extra_info)
    return render(request,'SensorsDataAPI/query_readings.html', dict)

def get_extra_info(readings):
    values_list = []
    extra_info = {}
    for reading in readings:
        reading_value = reading.reading_value 
        value_is_number = is_float(reading_value)
        if (value_is_number):
            values_list.append(float(reading_value))
    if len(values_list) != 0:
        value_range = get_value_range(values_list)
        mean_value = get_mean_value(values_list)
        max_records = get_max_records(values_list)
        min_records = get_min_records(values_list)
        extra_info = {
            'value_range': value_range,
            'mean_value': mean_value,
            'max_records': max_records,
            'min_records': min_records,
        }
    return extra_info

def is_float(reading_value):
    try:
        float(reading_value)
        return True
    except:
        return False

def get_value_range(values_list):
    min_value = min(values_list)
    max_value = max(values_list)
    value_range = (min_value,max_value)
    return value_range

def get_mean_value(values_list):
    mean_value = sum(values_list) / len(values_list)
    return mean_value

def get_max_records(values_list):
    num_of_records = min(10,len(values_list))
    values_list.sort(reverse = True)
    max_records = []
    for i in range(0,num_of_records):
        max_records.append(values_list[i])
    return max_records

def get_min_records(values_list):
    num_of_records = min(10,len(values_list))
    values_list.sort()
    min_records = []
    for i in range(0,num_of_records):
        min_records.append(values_list[i])
    return min_records

def add_sensor(request):
    sensor = Sensor(
    type = request.POST.get('sensor_type'), 
    vendor_name = request.POST.get('vendor_name'), 
    vendor_email = request.POST.get('vendor_email'),
    location = request.POST.get('location'),
    description = request.POST.get('description'))
    sensor.save()
    return HttpResponse(status=200)

def delete_sensor(request):
    sensor_id = request.POST.get('sensor_id')
    Sensor.objects.filter(sensor_id=sensor_id).delete()
    return HttpResponse(status=200)

def add_reading(request):
    reading = SensorReading(
    sensor = Sensor.objects.get(sensor_id = request.POST.get('sensor_id')), 
    reading_type = request.POST.get('reading_type'), 
    reading_value = request.POST.get('reading_value'), 
    reading_date = request.POST.get('reading_date'),
    description = request.POST.get('description'),
    reading_time = request.POST.get('reading_time'),)
    reading.save()
    return HttpResponse(status=200)

def delete_reading(request):
    reading_id = request.POST.get('reading_id')
    SensorReading.objects.filter(id=reading_id).delete()
    return HttpResponse(status=200)

def times_of_day(increment):
    times = []
    for hour in range(24):
        for minute in range(0, 60,increment):
            times.append('{:02d}:{:02d}'.format(hour, minute))
    return times

def get_filter_values(request):
    first_time = datetime.strptime(request.POST["first_time"],'%H:%M')
    second_time = datetime.strptime(request.POST["second_time"],'%H:%M')
    first_time = datetime.strftime(first_time,"%H:%M")
    second_time = datetime.strftime(second_time,"%H:%M")
    filter_values = {
        'sensor_type' : request.POST["sensor_type"],
        'location' : request.POST["location"],
        'first_time' : first_time,
        'second_time' : second_time,
        }
    return filter_values

def get_readings_filtered(filter_values):
    readings = SensorReading.objects.all().order_by('reading_date','reading_time')
    filtered_readings = []
    for reading in readings:
        if reading_matches_filters(reading, filter_values):
            filtered_readings.append(reading)
    return filtered_readings

def reading_matches_filters(reading,filter_values):
    matches_time = time_in_range(filter_values['first_time'],filter_values['second_time'],reading.reading_time)
    matches_type = sensor_is_type(reading.sensor.sensor_id,filter_values['sensor_type']) 
    matches_location = sensor_in_location(reading.sensor.sensor_id,filter_values['location'])
    if matches_time and matches_type and matches_location:
        return True
    else:
        return False

def time_in_range(first, second, reading_time):
    if first == second:
        return True
    if first < second:
        return first <= reading_time <= second
    else:
        return first <= reading_time or reading_time <= second

def sensor_is_type(sensor_id,sensor_type):
    sensors_of_type = Sensor.objects.filter(type = sensor_type).order_by().values_list('sensor_id',flat = True).distinct()
    if sensor_id in sensors_of_type:
        return True
    elif sensor_type == "All types":
        return True
    else:
        return False

def sensor_in_location(sensor_id, sensor_location):
    sensors_in_location = Sensor.objects.filter(location = sensor_location).order_by().values_list('sensor_id',flat = True).distinct()
    if sensor_id in sensors_in_location:
        return True
    elif sensor_location == "All locations":
        return True
    else:
        return False