import { Component, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { StudentService } from './student.service';
import { ProfileComponent } from './profile/profile.component';
import {OrganiserService} from './organiser.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'app';
  message: object;
  serverData: JSON;
  m: string;

  constructor(private httpClient: HttpClient, private organiser: OrganiserService) {
    this.organiser.currentMessage.subscribe(message => {this.message = message; console.log(this.message); this.show(); this.check();});
  }

  ngOnInit() {
  }

  show() {
    //console.log(this.student.currentMessage);
    if(this.message.hasOwnProperty('first_name')) {
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

  check() {
    if(Object.keys(this.message).length == 0) {
      return false;
    }
    else
      return true;
  }


}
