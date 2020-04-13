import { Component, OnInit, NgZone, Output } from '@angular/core';
import { StudentService } from '../student.service';
import { EventEmitter } from '@angular/core';
import { OrganiserService } from '../organiser.service';
import {Router} from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  templateUrl: './profile.component.html'
})

export class ProfileComponent implements OnInit {
  message: object;
  name: string;
  serverData: object;
  @Output() messageEvent = new EventEmitter();

  constructor(private organiser: OrganiserService, private ngZone: NgZone, public router: Router, private httpClient: HttpClient) {
    this.name = '';
  }

  ngOnInit() {
    this.organiser.currentMessage.subscribe(message => this.message = message);
    console.log(this.message);
    this.ngZone.run(() => {this.name = this.message['first_name'];});

    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }

  }

  get_events() {
    this.router.navigateByUrl('/allevents');
    };
}
