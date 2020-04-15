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
  styleUrls: [ 'event_details.component.css','../../../../node_modules/materialize-css/dist/css/materialize.min.css', '../../../../node_modules/bootstrap/dist/css/bootstrap.min.css']
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
  }


  /*reg(){
    var x=(<HTMLInputElement>document.getElementById("inp")).value;
    var mem= "[" + x + "]";
    //console.log(mem);
    this.httpClient.post('http://127.0.0.1:5000/student/checksize', {'team':mem,'student_id':this.message['s_id'],'e_id':this.message['e_id']}).subscribe(data => {
        this.chksize= data as JSON
        console.log(typeof(this.chk))
        console.log(this.chk)
        if (Object.keys(this.chksize).length == 0){

    this.httpClient.post('http://127.0.0.1:5000/student/checkteam', {'team':mem}).subscribe(data => {
        this.chk= data as JSON
        console.log(typeof(this.chk))
        console.log(this.chk)
        if (Object.keys(this.chk).length == 0){
              console.log("YEAH");

              this.httpClient.post('http://127.0.0.1:5000/student/checkmem', {'team':mem,'student_id':this.message['s_id'],'e_id':this.message['e_id']}).subscribe(data => {
                 this.chkagain= data as JSON
                  console.log(typeof(this.chkagain))
                  console.log(this.chk)
                  if (Object.keys(this.chkagain).length == 0){
                      console.log(this.message['s_id']);
                      this.httpClient.post('http://127.0.0.1:5000/student/regevent', {'student_id':this.message['s_id'],'event_name':this.ename,'team_members':mem}).subscribe(data => {
                              this.evres= data as JSON
                      });

                      document.getElementById("invalid").innerHTML="Registered! check your email";
                  }
                  else{
                      document.getElementById("invalid").innerHTML="One of your team members have already registered for this event.";
                  }
                });//second

                }//if

        else{
                  document.getElementById("invalid").innerHTML="Invalid team members";
        }


      });//first


    }
    else{
      document.getElementById("invalid").innerHTML="Team size exceeded!";
    }
  });
  }//reg

*/





 /*
  showorg(){
    this.httpClient.post('http://127.0.0.1:5000/student/orgdet', {'o_id':this.message['o_id']}).subscribe(data => {
          this.orgData= data as JSON;
          console.log("Organiser")
          console.log(this.orgData);
          if (Object.keys(this.orgData).length == 0){
           document.getElementById("orgn").innerHTML="Unavailable! Sorry.";
          }
          else{
            console.log("in else")
            var x=document.getElementById("org");
            console.log("print");
            //console.log(x,typeof(x));
            if (x.style.display === "none") {
               x.style.display = "block";
            }
            else {
              x.style.display = "none";
            }
          }
    });

    //var x=document.getElementById("org");
    //console.log("print2");
    //console.log(x,typeof(x));
  } */
//class



