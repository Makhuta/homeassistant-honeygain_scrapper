# Data scrapper for HoneyGain
Adds multiple sensors with information/statistics grabbed from HoneyGain account

## Installation

### Requirements:
Docker container [makhuta/honeygain-scrapper](https://hub.docker.com/r/makhuta/honeygain-scrapper) **installed**

1. Install this component by copying [these files](https://github.com/Makhuta/homeassistant-honeygain_scrapper/tree/main/custom_components/honeygain_scrapper) to `custom_components/honegain_scrapper/`.
2. **You will need to restart after installation for the component to start working.**

### Options

| key | default | required | description
| --- | --- | --- | ---
| url | | yes | Your HoneyGain docker container URL

### Sample for config needed in configuration.yaml:
```yaml
sensor:
  - platform: honeygain_scrapper
    url: YOUR_DOCKER_CONTAINER_URL
```