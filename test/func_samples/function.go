package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	// GET /test/result/golang_string
	fmt.Println("Hello, Golang!")

	// GET /test/result/golang.json
	greet := map[string]string{"hello": "golang"}
	j, _ := json.Marshal(greet)
	fmt.Println(string(j))
}
