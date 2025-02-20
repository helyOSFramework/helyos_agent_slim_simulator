# helyos_agent_slim_simulator

It simulates an agent in the helyOS framework. It can be used for front-end development or for testing path planning algorithms.

## Getting started



### Run Natively

1. Install requirements

   ``` bash
   pip install -r requirements.txt
   ```

2. Configure the simulator by placing a `.env` file in the `src` folder as shown in `./example/.env` (see [Configuration](#configuration)).

3. Run the simulator
   ``` python
   python main.py
   ```


### Deploy with Docker Compose
Alternatively, use a docker-compose.yml as shown in the `./example` folder. 
Configure the agent using the `./example/.env` file. 

``` bash
cd example
docker compose up
```
For development purposes, the source code can be mounted into the container

``` yaml
# docker-compose.yml
volumes:
   - ../src:/app 
```
Now, when running `docker compose up`, changes in the `src` directory will reflect immediately in the container. Alternatively, build a new docker image and link it in the `docker-compose.yml`. 


## Building a Docker Image

To build a Docker image for the application, use one of the following commands:

1. **Standard Build**:

```bash 
docker build --no-cache -t helyosframework/helyos_agent_slim_simulator:test .
```

2. **Multi-Platform Build**:

``` bash
docker buildx build --platform linux/amd64 -t helyosframework/helyos_agent_slim_simulator:x86 --no-cache . --load
```

## Assignment data formats

The agent simulator can receive and follow paths sent by helyOS. It supports the following assignment data formats. 

### Trajectory

```python
assignment = { "operation": "driving", "trajectory": [{"x": float, "y": float, "orientations":List[float], time:float}, ...] }

```
### Destination point
``` python
assignment = { "operation": "driving", "destination": {"x": float, "y": float, "orientations":List[float]}  }
```

### AutoTruck-TruckTrix path format

https://app.swaggerhub.com/apis-docs/helyOS/Tructrix_API/4.0#/TrucktrixTrajectory


## Instant actions
Besides the helyOS-required instant actions (mission reserve, mission release and cancel),
we have implemented additional instant actions triggered by the following strings:

* "pause" or "resume" : pause/resume a running assignment.
* "tail lift up" or "tail lift down": change the value of the tail lift sensor.
* "headlight on" or "headlight off": change the value of the headlight sensor.

## Customizations

The `/src/customizations` folder contains scripts and configurations that allow for further customization of the simulator:

| File                          | Description                                        |
| ----------------------------- | -------------------------------------------------- |
| `agent_sensors.py`            | Defines the sensor data for the simulated agent.   |
| `connected_tool_sensors.py`   | Manages sensor data for tools connected to the agent. |
| `custom_instant_actions.py`   | Implements additional instant actions for the simulator. |
| `shared_data.pys`             | Contains geometric configurations for the simulation. |
| `geometry.json`               | Customize the sensors initial data and access communication channels. |


## Configuration
The simulator is configured by the following environment variables:

| VARIABLE | DESCRIPTION |
| --- | --- |
| UUID | String with unique identifcation code of agent (set to RANDOM_UUID for auto-generated uuids) |
| REGISTRATION_TOKEN | Allow agent to check in without credentials even if not registered in helyOS |
| NAME | Agent name |
| YARD_UID | Yard Identifier |
| UPDATE_RATE | Frequency of published messages (Hz) |
| --- | --- |
| PATH_TRACKER |  ideal (arb. unit), stanley (mm), straight_to_destination(arb.unit)|
| ASSIGNMENT_FORMAT | fixed, trajectory, destination, trucktrix-path |
| VEHICLE_PARTS | Number of parts. eg. truck with trailer: 2 |
| --- | --- |
| X0 | Initial horizontal position (arb. unit, dep. PATH_TRACKER)|
| Y0 | Initial vertical position (arb. unit, dep. PATH_TRACKER)|
| ORIENTATION | Initial orientation in mrads |
| VELOCITY | Driving velocity 0 to 10. (arb. unit) |
| --- | --- |
| RBMQ_HOST | Adress of the HelyOS RabbitMQ Server (e.g  rabbitmq.server.com, localhost, default: local_message_broker, see [RabbitMQ Server Connection](#rabbitmq-server-connection))  |
| RBMQ_VHOST | Virtual host of RabbitMQ   |
| RBMQ_PORT | HelyOS RabbitMQ Port (e.g.,5671, 5672, 1883, 8883, default:5672)  |
| RBMQ_USERNAME | Agent RabbitMQ account name |
| RBMQ_PASSWORD | Agent RabbitMQ account password  |
| PROTOCOL | "AMQP" or "MQTT" (default: AMPQ)  |
| ENABLE_SSL | True or False (default: False)  |
| CACERTIFICATE_FILENAME | Location of the server host CA certificate. Only relevant if ENABLE_SSL=True. (default: ca_certificate.pem) | 


Optional environment variable for the `stanley` path tracker:

| VARIABLE | DESCRIPTION |
| --- | --- |
| STANLEY_K | control gain (default: 1) |
| STANLEY_KP | speed proportional gain (default: 0.5)|
| STANLEY_L |  Wheel base of vehicle length (m) (default: 2.9) |
| STANLEY_MAXSTEER | (rad) max steering angle (default: 12)|
| --- | --- |


Ref:
    - [Stanley: The robot that won the DARPA grand challenge](http://isl.ecst.csuchico.edu/DOCS/darpa2005/DARPA%202005%20Stanley.pdf)
    - [Autonomous Automobile Path Tracking](https://www.ri.cmu.edu/pub_files/2009/2/Automatic_Steering_Methods_for_Autonomous_Automobile_Path_Tracking.pdf)

## RabbitMQ Server Connection

The `RBMQ_HOST` variable specifies the RabbitMQ server address for the helyOS control tower. Below are example configurations for different deployment scenarios:

- **Docker Deployment**:  
  For a RabbitMQ server running as a Docker service named `local_message_broker`, set `RBMQ_HOST` to `local_message_broker`. In this scenario, ensure that the agent simulator operates within the same Docker network as the RabbitMQ broker (refer to `./example/docker_compose.yml` for network configuration details).

- **Local Development**:  
  If you choose to run the agent simulator natively on your machine and you run a locally hosted RabbitMQ server, set `RBMQ_HOST` to `localhost`.


### License

This project is licensed under the MIT License.