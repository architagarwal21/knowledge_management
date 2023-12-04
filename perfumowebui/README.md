# demogetdata 

This is an incomplete but simple information application intended to be run on localhost port 3000. It retrieves data from a single web page and saves those data in a plain text file with the **html** extension. Revisions of the app are left as exercises for students. See the list at the end of this writeup.

Students new to Go can learn more about the language at the website [*Learning Go for Data Science*](https://msdsgo.netlify.app/). 

Working in a command or terminal window, the client/user runs the go program:
```
go run main.go
```
This should provide a message in the command/terminal window indicating that the web server has started. The user then brings up a browser window and enters the localhost and port address in the request window:
```
localhost:3000
```
This app asks the user to enter a web address (URL), gathers data from that web page, and saves those data in a local HTML file under the **webpages** directory on the user's computer. The user closes the server by typing control/command C.

This application uses server-side rendering and the Go standard library [html/template](https://pkg.go.dev/html/template). This demo uses HTML without any CSS styling. The focus is on http server operations.

Information about Go templates is available from various sources, including
- Go documentation at [https://golang.org/pkg/html/template](https://golang.org/pkg/html/template)
- Go tutorial at [https://go.dev/doc/articles/wiki/#tmp_6](https://go.dev/doc/articles/wiki/#tmp_6)
- Jon Calhoun's introduction to templates at [https://www.calhoun.io/html-templates-in-go](https://www.calhoun.io/html-templates-in-go)

Information about HTML is available at [https://www.w3schools.com/html/](https://www.w3schools.com/html/) and [https://www.rapidtables.com/web/html/html-codes.html](https://www.rapidtables.com/web/html/html-codes.html). Of special interest for this application is the [Mozilla documentation about HTML forms](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form).

Additional information about web apps and server-side rendering is available under *Building Systems and Services* on the website [*Learning Go for Data Science*](https://msdsgo.netlify.app).

#### Exercises for students
- Currently, the app reports an error with the server still running, and the user closes the server by typing control/command C. Find a way to gracefully shut down the server after the data from one web page have been saved. Hint: Use [func (*Server) Shutdown](https://pkg.go.dev/net/http#Server.Shutdown) and the [context](https://pkg.go.dev/context) package.
- Add navigation and routing to the app, so the **Enter web address** form is on a separate web page.
- Add a second HTML template page to display the data from the web page on the screen in addition to saving the data to a file. Along with the displayed data, provide a button that users can click to begin the process anew, returning to the page asking for the web page URL.
- Use Go **html/template** more fully, so the url from **Enter web address** is a template variable.
- Place the the **Enter web address** form in a loop, so data may be collected from many web pages and stored in separate files under the **webpages** directory. Provide a unique, valid file name for each saved file based on text from each web page URL.
- Rather than placing the entire HTML body of the web page in the file stored under the **webpages** directory, scape the body text, dropping HTML tags, file formatting, and data of little information value. The thinking here is that collected data from web pages will be used in a subsequent information app or knowledge base. Hint: Useful text is likely to be found within heading and paragraph tags, rather than anchor, style, and script tags.
- Add unit tests using [testing](https://pkg.go.dev/testing) from the Go standard library.
- Add styling to the site with cascading style sheets (CSS), [Tailwind](https://tailwindcss.com/), or a components library (in CSS or Tailwind). Ensure that the site is responsive, so it looks good and works well on desktop, tablet, and smartphone displays. Note: Tailwind and Tailwind-compliant components are responsive, as are established CSS component libraries such as [Bootstrap](https://getbootstrap.com/) and [Material Design](https://m3.material.io/).
- Further develop the app so it becomes a user interface to web crawling and scraping, perhaps with the [Colly scraping framework](https://pkg.go.dev/github.com/gocolly/colly/v2).


