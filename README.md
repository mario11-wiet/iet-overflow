<div align="center">
<img src="https://github.com/mario11-wiet/iet-overflow/blob/main/iet_overflow/static/images/icons/readme/logo.png" width=auto height=100px alt="Menu">
</div>

# Technology

<hr>

<ul>
  
<li> 
  
### Django 4.0
    
</li>
   
<li> 
  
### PostgreSQL
  
</li>

<li> 
  
### Docker
  
</li>
    
</ul>

<hr>

# How to run

## Cloning the repository "

```
https://github.com/mario11-wiet/iet-overflow.git
```

## Move into the directory :

```
cd iet_overflow
```

## Start project's containers :

```
docker-compose up
```

## Open a web browser and type :

```
http://localhost:8000/
```

## If the server did not start then :

### If you use docker in terminal :

#### Enter the container :

```
docker exec -it $(docker ps --filter "name=iet_overflow_web"  --format "{{.ID}}") bash
```

#### Run a server (if you are in container) :

```
python manage.py runserver
```

# App photos

<div align="center">

## Home Page
  
<img src="https://github.com/mario11-wiet/iet-overflow/blob/main/iet_overflow/static/images/icons/readme/home.png" width=1000px height=auto alt="Menu">
  
## Room Page
  
<img src="https://github.com/mario11-wiet/iet-overflow/blob/main/iet_overflow/static/images/icons/readme/room.png" width=1000px height=auto alt="Menu">

## Profile Page
  
<img src="https://github.com/mario11-wiet/iet-overflow/blob/main/iet_overflow/static/images/icons/readme/profile.png" width=1000px height=auto alt="Menu">

</div>

<br />

<br />

<br />

<br />

# Mobile 📱 

<div align="center">

## Mobile Home Page
  
<img src="https://github.com/mario11-wiet/iet-overflow/blob/main/iet_overflow/static/images/icons/readme/mobile.png" width=400px height=auto alt="Menu">

</div>
