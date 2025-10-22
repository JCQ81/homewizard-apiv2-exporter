#!/usr/bin/env python3

import sys
import numbers
import requests
from flask import Flask, request, Response
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import GaugeMetricFamily, Gauge

import hwhelper

app = Flask(__name__)
config = hwhelper.get_config()
device = {}


class OnDemandCollector:
    def __init__(self, target):
        self.target = target

    def collect(self):
        global config
        global device
        
        # Check if a token is available        
        token = None    
        if "cloud" in config and "token" in config["cloud"]:
            token = config["cloud"]["token"]
        if "targets" in config and isinstance(config["targets"], list):
            for target in config["targets"]:
                if "host" in target and target["host"] == self.target and "token" in target:
                    token = target["token"]
        
        # Set headers          
        hdrs = hwhelper.get_headers(token=token)
                    
        # Check API version availability
        if self.target not in device:
            device[self.target] = { "v1": None, "v2": None }
            try:
                response = requests.get(f"http://{self.target}/api", timeout=2)
                device[self.target]["v1"] = response.json()
            except requests.RequestException:
                pass
            if token is not None:
                try:
                    response = requests.get(f"https://{self.target}/api", headers=hdrs, timeout=5, verify=False)
                    device[self.target]["v2"] = response.json()
                except requests.RequestException:
                    pass
            print(f"Connected to device: {self.target}\n{device[self.target]}")    
        

        # Get metrics
        metrics = {}
        for api_version in ["v1", "v2"]:
            if device[self.target][api_version] is not None:
                product_type = "unknown"
                if "product_type" in device[self.target][api_version]:
                    product_type = device[self.target][api_version]["product_type"]
                    
                if api_version == "v1":
                    response = requests.get(f"http://{self.target}/api/v1/data", timeout=5)
                else:
                    response = requests.get(f"https://{self.target}/api/measurement", headers=hdrs, timeout=5, verify=False)
                    
                for metric, value in response.json().items():
                    metrics[metric] = (value, product_type, api_version)
        
        # Return metrics
        for name, data in metrics.items():
            value, product_type, api_version = data
            if isinstance(value, numbers.Number):
                metric = GaugeMetricFamily(name, "", labels=["product_type", "api_version"])
                metric.add_metric([product_type, api_version], value)
                yield metric


@app.route("/metrics")
def metrics():
    target = request.args.get("target", "default")
    registry = CollectorRegistry()
    registry.register(OnDemandCollector(target))
    result = generate_latest(registry)
    return Response(result, mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
