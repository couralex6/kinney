// -*- Mode: Go; indent-tabs-mode: t -*-
//
// Copyright (C) 2018 Canonical Ltd
// Copyright (C) 2018-2019 IOTech Ltd
//
// SPDX-License-Identifier: Apache-2.0

// This package provides a simple example implementation of
// ProtocolDriver interface.
//
package driver

import (
	"fmt"
	"time"

	dsModels "github.com/edgexfoundry/device-sdk-go/pkg/models"
	"github.com/edgexfoundry/go-mod-core-contracts/clients/logger"
	contract "github.com/edgexfoundry/go-mod-core-contracts/models"
)

type SimpleDriver struct {
	lc           logger.LoggingClient
	asyncCh      chan<- *dsModels.AsyncValues
	currentLoad float64
}

// Initialize performs protocol-specific initialization for the device
// service.
func (s *SimpleDriver) Initialize(lc logger.LoggingClient, asyncCh chan<- *dsModels.AsyncValues) error {
	s.lc = lc
	s.asyncCh = asyncCh
	return nil
}

// HandleReadCommands triggers a protocol Read operation for the specified device.
func (s *SimpleDriver) HandleReadCommands(deviceName string, protocols map[string]contract.ProtocolProperties, reqs []dsModels.CommandRequest) (res []*dsModels.CommandValue, err error) {
	s.lc.Info(fmt.Sprintf("SimpleDriver.HandleReadCommands: protocols: %v resource: %v attributes: %v", protocols, reqs[0].DeviceResourceName, reqs[0].Attributes))


	res = make([]*dsModels.CommandValue, 1)
	now := time.Now().UnixNano()
	if len(reqs) == 1 {

		if reqs[0].DeviceResourceName == "getLoad" {
			s.currentLoad = float64(10)
			cv, _ := dsModels.NewFloat64Value(reqs[0].DeviceResourceName, now, s.currentLoad)
			res[0] = cv
			s.lc.Info(fmt.Sprintf("TEST TEST TEST: %v", s.currentLoad ))
		}
	}

	return res, nil
}

// HandleWriteCommands passes a slice of CommandRequest struct each representing
// a ResourceOperation for a specific device resource.
// Since the commands are actuation commands, params provide parameters for the individual
// command.
func (s *SimpleDriver) HandleWriteCommands(deviceName string, protocols map[string]contract.ProtocolProperties, reqs []dsModels.CommandRequest,
	params []*dsModels.CommandValue) error {
	s.lc.Debug(fmt.Sprintf("SimpleDriver.HandleWriteCommands: protocols: %v, resource: %v, parameters: %v", protocols, reqs[0].DeviceResourceName, params))

	fmt.Printf("%v", deviceName)

	fmt.Printf("%v", protocols)

	fmt.Printf("%v", reqs)

	// var err error
	// if len(reqs) == 1 {
	// 	if s.switchButton, err = params[0].BoolValue(); err != nil {
	// 		err := fmt.Errorf("SimpleDriver.HandleWriteCommands; the data type of parameter should be Boolean, parameter: %s", params[0].String())
	// 		return err
	// 	}
	// } else if len(reqs) == 3 {
	// 	for i, r := range reqs {
	// 		switch r.DeviceResourceName {
	// 		case "Xrotation":
	// 			if s.xRotation, err = params[i].Int32Value(); err != nil {
	// 				err := fmt.Errorf("SimpleDriver.HandleWriteCommands; the data type of parameter should be Int32, parameter: %s", params[i].String())
	// 				return err
	// 			}
	// 		case "Yrotation":
	// 			if s.yRotation, err = params[i].Int32Value(); err != nil {
	// 				err := fmt.Errorf("SimpleDriver.HandleWriteCommands; the data type of parameter should be Int32, parameter: %s", params[i].String())
	// 				return err
	// 			}
	// 		case "Zrotation":
	// 			if s.zRotation, err = params[i].Int32Value(); err != nil {
	// 				err := fmt.Errorf("SimpleDriver.HandleWriteCommands; the data type of parameter should be Int32, parameter: %s", params[i].String())
	// 				return err
	// 			}
	// 		}
	// 	}
	// }

	return nil
}

// Stop the protocol-specific DS code to shutdown gracefully, or
// if the force parameter is 'true', immediately. The driver is responsible
// for closing any in-use channels, including the channel used to send async
// readings (if supported).
func (s *SimpleDriver) Stop(force bool) error {
	// Then Logging Client might not be initialized
	if s.lc != nil {
		s.lc.Debug(fmt.Sprintf("SimpleDriver.Stop called: force=%v", force))
	}
	return nil
}

// AddDevice is a callback function that is invoked
// when a new Device associated with this Device Service is added
func (s *SimpleDriver) AddDevice(deviceName string, protocols map[string]contract.ProtocolProperties, adminState contract.AdminState) error {
	s.lc.Debug(fmt.Sprintf("a new Device is added: %s", deviceName))
	return nil
}

// UpdateDevice is a callback function that is invoked
// when a Device associated with this Device Service is updated
func (s *SimpleDriver) UpdateDevice(deviceName string, protocols map[string]contract.ProtocolProperties, adminState contract.AdminState) error {
	s.lc.Debug(fmt.Sprintf("Device %s is updated", deviceName))
	return nil
}

// RemoveDevice is a callback function that is invoked
// when a Device associated with this Device Service is removed
func (s *SimpleDriver) RemoveDevice(deviceName string, protocols map[string]contract.ProtocolProperties) error {
	s.lc.Debug(fmt.Sprintf("Device %s is removed", deviceName))
	return nil
}
