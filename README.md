
# Outsider: Event Management Website
An enhanced, user friendly web based application where users can find and register for events created by organisers. Implemented with Angular and Flask, *Outsider* offers two portals: one for the organisers and another for the Users/Students. Both of these portals are account based. 
The Organiser can create events, allocate funds, view the profits made for his/her events. 
The student/user can register for these events, view similar users, view the events they have registered for, etc. 

Apart from these core functionalities, *Outsider* also provides event related statistics on both sides, for the organiser/student to be able to view trends and make inferences. 
The performance of the *Outsider* Application was tested using <a href = "https://locust.io/">Locust</a>
### Unique Selling Point
*Outsider* as a portal provides a list of similar users on every user’s profile. This helps them connect with other people who have similar interests, which is not available on many of the event management websites that we presently see.
The data visualisations on our website also form a unique aspect that guide the organiser and the user/student.

### Intelligent Functionality
1. Collaborative filtering -cosine similarity to find the most similar users based on the events    he/she has registered for. This helps users connect with each other, and  to make teams with like minded people.
1. Data analytics:
	1.  Organiser side: Graphs displaying Number of registrations per event, profit made per event, etc. 
	1.  User side: Pie charts displaying the most popular events, popular event categories from their hobbies, etc. 
  
## Implementation Details
### Technologies
<ul>
  <li> Frontend: Angular (HTML, CSS, TypeScript)</li>
  <li> Backend: Flask (Python)</li>
  <li> Database: SQLite </li>
 </ul>

### Techniques
<ul><li>RESTful APIs <br/>
	Every functionality of our website is written as  a separate microservice with flask. Each time a microservice is required, we make a call to the corresponding API.	
</li>
<li>	AJAX pattern - submission throttling <br/>
    	Auto-complete mechanism for event searching on the user/student side.
</li>
</ul>

### Files/Folders
1. `server.py` implements the backend functionalities using flask
1. `ml.py` implements the intelligent functionalities
1. `src` folder contains the Angular code for the application

## Instructions to Run
1. Setup your Angular environment: https://angular.io/guide/setup-local 
1. Create a new app with the following command: `ng new outsider-app` 
1. Clone this repository: `git clone "https://github.com/ArchPrak/Outsider/"`. Copy-paste the repository content into your app workspace directory.  
1. Go into the workspace directory with the following command: `cd outsider-app` 
1. Run the <i>Outsider</i> application with the following command: `ng serve` 
1. Open another terminal and go into this workspace directory. Run the server file with: `python3 server.py`. This hosts the flask server on port 5000.
1. Navigate to `http://localhost:4200/` on your browser. The app will automatically reload if you change any of the source files.
 
   
This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 9.1.0.

## Additional Information about Angular
#### Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

#### Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

#### Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

#### Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

#### Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
