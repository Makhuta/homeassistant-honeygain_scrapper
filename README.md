# Data scrapper for HoneyGain
Adds multiple sensors with information/statistics grabbed from HoneyGain account

## Installation

1. Install this component by copying [these files](https://github.com/Makhuta/homeassistant-honeygain_scrapper/tree/main/custom_components/honeygain_scrapper) to `custom_components/honegain_scrapper/`.
2. **You will need to restart after installation for the component to start working.**

### Options

| key | default | required | description
| --- | --- | --- | ---
| username | | yes | Your HoneyGain username
| password | | yes | Your HoneyGain password

### Sample for config needed in configuration.yaml:
```yaml
sensor:
  - platform: honeygain_scrapper
    username: YOUR_USERNAME
    password: YOUR_PASSWORD
```