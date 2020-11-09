import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, ReactiveFormsModule, EmailValidator } from '@angular/forms';
import { Router, Routes, RouterModule } from '@angular/router';
import { OrganiserService } from 'src/app/organiser.service';


@Component({
  templateUrl: './create_event.component.html',
  styleUrls: ['create_event.component.css', '../../../../node_modules/materialize-css/dist/css/materialize.min.css', '../../../../node_modules/bootstrap/dist/css/bootstrap.min.css']
})

export class CreateEvent {

  eventForm: FormGroup;
  serverData: JSON;
  message: object;

  constructor(private httpClient: HttpClient, public router: Router, private organiser : OrganiserService) {
    this.eventForm = new FormGroup({
      event_name: new FormControl(''),
      event_type: new FormControl(''),
      max_par: new FormControl(''),
      fee: new FormControl(''),
      max_teams: new FormControl(''),
      event_date: new FormControl(''),
      event_venue: new FormControl(''),
      funds: new FormControl('')
    });
  }

  ngOnInit() {
    this.organiser.currentMessage.subscribe(message => this.message = message);
    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
  }

  newEvent() {
    var reqData = {'funds': this.eventForm.value['funds'],'o_id': this.message['o_id'],'event_venue': this.eventForm.value['event_venue'],'event_date': this.eventForm.value['event_date'],'event_name': this.eventForm.value['event_name'], event_type: this.eventForm.value['event_type'], 'max_par': this.eventForm.value['max_par'] , 'fee': this.eventForm.value['fee'], 'max_teams': this.eventForm.value['max_teams']};
    if(reqData["event_name"].length != 0 && reqData["event_type"].length != 0 && reqData["max_par"].length != 0 && reqData["fee"].length != 0 && reqData["max_teams"].length != 0) {
      this.httpClient.post('http://127.0.0.1:5000/newevent', reqData ).subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
      this.router.navigateByUrl('/profile');
      })
    }
  }
}
