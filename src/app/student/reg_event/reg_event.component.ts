import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, ReactiveFormsModule } from '@angular/forms';
import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';
import { Component, OnInit, NgZone, Output,EventEmitter } from '@angular/core';


@Component({
  selector: 'reg-event',
  templateUrl: './reg_event.component.html'
})

export class RegEvent {
    message: object;
    serverData: object;

    @Output() messageEvent = new EventEmitter();

    constructor (private student: StudentService, private ngZone: NgZone,private httpClient: HttpClient, private data: StudentService, public router: Router) {
                //this.regEventsForm = new FormGroup({});
    }

    ngOnInit(){

            this.student.currentMessage.subscribe(message => this.message = message);
            this.httpClient.get('http://127.0.0.1:5000/student/dispevents')
            .subscribe(result => {
                this.serverData = result ;
                if (Object.keys(this.serverData).length === 0){
                    document.getElementById("ev").innerHTML="All events are currently full :/ Come back soon!";
                }

              },
              error => console.error(error)
            );
    }

    reg_event(event) {
        var o_id=event[3];
        var e_id=event[0];
        this.message["o_id"]=o_id;
        this.message["e_id"]=e_id;
        this.student.changeMessage(this.message);
        console.log("Modified mesg:");
        console.log(this.message);
        this.router.navigateByUrl("/eventdet");

    }

}

