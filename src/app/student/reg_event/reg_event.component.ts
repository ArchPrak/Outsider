import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, ReactiveFormsModule } from '@angular/forms';
import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';
import { Component, OnInit, NgZone, Output,EventEmitter } from '@angular/core';
import { EventDet } from '../event_details/event_details.component';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';


@Component({
  selector: 'reg-event',
  templateUrl: './reg_event.component.html',
  styleUrls: [ '../../../../node_modules/materialize-css/dist/css/materialize.min.css']
})

export class RegEvent {
    message: object;
    serverData: object;

    @Output() messageEvent = new EventEmitter();

    constructor (private student: StudentService, private ngZone: NgZone,private httpClient: HttpClient, private data: StudentService, public router: Router, public dialog: MatDialog) {
                //this.regEventsForm = new FormGroup({});
    }

    ngOnInit(){

      this.student.currentMessage.subscribe(message => this.message = message);
      if('s_id' in this.message) {
        this.httpClient.get('http://127.0.0.1:5000/student/dispevents')
        .subscribe(result => {
            this.serverData = result ;
            console.log(this.serverData);
            if (Object.keys(this.serverData).length === 0){
                document.getElementById("ev").innerHTML="All events are currently full :/ Come back soon!";
            }

          },
          error => console.error(error)
        );
      }
      else {
          this.router.navigateByUrl('/login');
      }
    }

    reg_event(event) {

        var o_id=event[3];
        var e_id=event[0];
        this.message["o_id"]=o_id;
        this.message["e_id"]=e_id;
        this.student.changeMessage(this.message);
        //console.log("Modified mesg:");
        //console.log(this.message);

        const dialogRef = this.dialog.open(EventDet, {
          width: '300px'
        })
        dialogRef.afterClosed().subscribe(result => {
          console.log('The dialog was closed');
          this.ngOnInit();
        });


        //this.router.navigateByUrl("/eventdet");
    }

}
