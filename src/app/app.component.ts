import { Component, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { StudentService } from './student.service';
import { ProfileComponent } from './profile/profile.component';
import {OrganiserService} from './organiser.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css', '../../node_modules/materialize-css/dist/css/materialize.min.css']
})

export class AppComponent {
  title = 'app';
  message: object;
  serverData: JSON;
  message1: object;
  serverData3:object;
  serverData2:string[];
  searchText:string;

  constructor(private httpClient: HttpClient, private organiser: OrganiserService, private student: StudentService, public router:Router) {
    this.organiser.currentMessage.subscribe(message => {this.message1 = message; console.log(this.message); });
    this.student.currentMessage.subscribe(message1 => {this.message = message1; console.log(this.message); });
  }

  ngOnInit() {
    this.message = {}
    this.message1 = {}
    this.httpClient.get('http://127.0.0.1:5000/student/getevents',).subscribe(data => {
      this.serverData2 = data as string[];

      console.log(this.serverData2)});
  }

  show() {
    //console.log(this.student.currentMessage);
    if('first_name' in this.message1 && 'o_id' in this.message1) {
      return true;
    }
    else
      return false;
  }

  setempty() {
    this.organiser.changeMessage({});
    //console.log(this.student.currentMessage);
    this.show();
  }

  show1() {
    if('first_name' in this.message && 's_id' in this.message) {
      return true;
    }
    else
      return false;
  }

  searchevent()
  {
    this.httpClient.post('http://127.0.0.1:5000/student/searchevents',{'name':this.searchText}).subscribe(data => {
      this.serverData3 = data as JSON;
      var bleh = this.serverData3[0][0];
      console.log(bleh);
      this.message["e_id"] = bleh ;
      this.message["o_id"] = this.serverData3[0][1]
      this.student.changeMessage(this.message);
      console.log("works");
      this.router.navigateByUrl("/eventdet");
      //console.log(this.serverData4);
    });
  }

}
