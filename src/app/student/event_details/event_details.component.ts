import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';
import {DispOrg} from '../display_org/display_org.component';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { TeamInput } from '../team_input/team_input.component';

import { AfterReg} from '../after_reg/after_reg.component';


@Component({
  selector: 'one-event',
  templateUrl: './event_details.component.html',
  styleUrls: ['../../../../node_modules/materialize-css/dist/css/materialize.min.css', '../../../../node_modules/bootstrap/dist/css/bootstrap.min.css']
})

export class EventDet {
  message: object;
  serverData:object;
  eventData: object;
  orgData:object;
  past :String[];
  upcoming :String[];
  chk :object;
  chksize:object;
  chkagain  : object;
  ename :String;
  evres: object;

  constructor(private httpClient: HttpClient, private data: StudentService, public router: Router,public dialog: MatDialog) {

  }

  ngOnInit() {
    this.data.currentMessage.subscribe((message) => this.message = message);
    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
    else {
      this.httpClient.post('http://127.0.0.1:5000/student/eventdet', {'e_id':this.message['e_id']}).subscribe(data => {
        this.eventData= data as JSON;
        this.ename=this.eventData[0][2];
        console.log("EVENT NAME:");
        console.log(this.ename);

      });

    }
  }
  showorg(){

    const dialogRef = this.dialog.open(DispOrg, {
      width: '300px'
    })
  }

  teaminp(){

    const dialogRef = this.dialog.open(TeamInput, {
      width: '300px'
    })
  }



  regevent(){
      const dialogRef = this.dialog.open(AfterReg, {
        width: '300px'
      })


}
goback() {
  this.dialog.closeAll();
}
}
