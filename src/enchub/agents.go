package main

import (
	"fmt"
	"strings"
	"time"
)

type Agent struct {
	ID     string
	Name   string
	Role   string
	Status string
}

var ActiveAgents = []Agent{
	{ID: "aura-1", Name: "Aura-1", Role: "Perception", Status: "Online"},
	{ID: "nexus-7", Name: "Nexus-7", Role: "Orchestration", Status: "Online"},
	{ID: "vortex-3", Name: "Vortex-3", Role: "Compliance", Status: "Online"},
}

func GetAgent(id string) *Agent {
	for i := range ActiveAgents {
		if ActiveAgents[i].ID == id {
			return &ActiveAgents[i]
		}
	}
	return nil
}

func HandleCommand(agentID string, cmd string) string {
	agent := GetAgent(agentID)
	if agent == nil {
		return fmt.Sprintf("Error: Agent %s not found.", agentID)
	}

	cmd = strings.TrimSpace(strings.ToLower(cmd))
	timestamp := time.Now().Format("15:04:05")

	switch cmd {
	case "/status":
		return fmt.Sprintf("[%s] %s: Status is %s. All systems nominal.", timestamp, agent.Name, agent.Status)
	case "/reboot":
		return fmt.Sprintf("[%s] %s: Rebooting subsystem... Please hold.", timestamp, agent.Name)
	case "/axiom":
		return fmt.Sprintf("[%s] %s: Current Axiom compliance: 100%%. No violations detected.", timestamp, agent.Name)
	default:
		return fmt.Sprintf("[%s] %s: Received command '%s'. Executing...", timestamp, agent.Name, cmd)
	}
}
