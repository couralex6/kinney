// -*- Mode: Go; indent-tabs-mode: t -*-
//
// Copyright (C) 2017-2018 Canonical Ltd
// Copyright (C) 2018-2019 IOTech Ltd
//
// SPDX-License-Identifier: Apache-2.0

// This package provides a simple example of a device service.
package main

import (
	"github.com/edgexfoundry/device-sdk-go/pkg/startup"
	"github.com/CamusEnergy/kinney/controller/ev-charger-device-service/driver"
)

const (
	version     string = "1.0.0"
	serviceName string = "ev-charger-device-service"
)

func main() {
	sd := driver.SimpleDriver{}
	startup.Bootstrap(serviceName, version, &sd)
}
