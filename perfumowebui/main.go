// Listing 3.1
package main

import (
	"fmt"
	"html/template"

	//"io"
	"log"
	"net/http"

	//"os"
	"path/filepath"
)

func processInput(input string) string {
	// Example processing: just return a message with the input
	return fmt.Sprintf("Processed input: %s", input)
}

func pageHandler(w http.ResponseWriter, r *http.Request) {
	welcomePath := filepath.Join("templates", "perfume.gohtml")
	welcomeTemplate, err := template.ParseFiles(welcomePath)
	if err != nil {
		log.Printf("Unable to parse welcome template file: %v", err)
		http.Error(w, "Unable to parse welcome template file", http.StatusInternalServerError)
		return
	}
	err = welcomeTemplate.Execute(w, nil)
	if err != nil {
		log.Printf("Unable to execute welcome template: %v", err)
		http.Error(w, "Unable to execute welcome template", http.StatusInternalServerError)
		return
	}

	// //query := r.FormValue("query")
	// log.Println("Search Query:") // Print the query to the server log
	if r.Method == "POST" {
		if err := r.ParseForm(); err != nil {
			http.Error(w, "ParseForm() error", http.StatusInternalServerError)
			fmt.Println("What's happening?")
			fmt.Println(err)
			return
		}
	} else if r.Method == "GET" {
		// Handle GET request
		// Typically, you would retrieve the query from r.URL.Query()
		query := r.URL.Query().Get("search")
		log.Println("Search Query:", query)
		// Respond as necessary
		w.Write([]byte("You searched for: " + query))
		return

	} else {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

}

func main() {
	http.HandleFunc("/", pageHandler)
	fmt.Println("Starting the web server on localhost port 3000, localhost:3000")

	apiURL := "https://api.openai.com/chatgpt"

    // Create your payload
    payload := Payload {
        Prompt: "Identify the perfume notes, perfume scent group, perfume brand and assume that the required perfume rating is more than 3/5",
    }

    // Marshal the payload into JSON
    payloadBytes, err := json.Marshal(payload)
    if err != nil {
        log.Fatalf("Error marshalling payload: %v", err)
    }

    // Create a new request using http
    req, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(payloadBytes))
    if err != nil {
        log.Fatalf("Error creating request: %v", err)
    }

    // Add headers, e.g., Content-Type and Authorization (API Key)
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Authorization", "Bearer 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")

    // Create a Client and send the request
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        log.Fatalf("Error sending request to API endpoint: %v", err)
    }
    defer resp.Body.Close()

    // Read the response body
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        log.Fatalf("Error reading response body: %v", err)
    }

    // Unmarshal the response body into the Response struct
    var response Response
    err = json.Unmarshal(body, &response)
    if err != nil {
        log.Fatalf("Error unmarshalling response body: %v", err)
    }

    // Print the response
    fmt.Println("Response from ChatGPT:", response.Answer)
}

	err := http.ListenAndServe(":3000", nil)
	if err != nil {
		log.Printf("Unable to start web server or server crash: %v", err)
		return
	}

	//ChatGPT API Key : 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

}
