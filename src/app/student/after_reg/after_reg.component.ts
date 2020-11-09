import {Component, Inject} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import {MatTableModule} from '@angular/material/table';

import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';
import { ArrayDataSource } from '@angular/cdk/collections';

@Component({
  selector: 'after-reg',
  templateUrl: 'after_reg.component.html',

})

export class AfterReg {
  orgData: object;
  noOrg : String;
  serverData:object;
  message:object;
  rid: Array<number>;
  sid: Array<number>;
  sname: Array<string>;
  team_mates: Array<Array<string>>;
  msg:string
  constructor(public dialogRef: MatDialogRef<AfterReg>, private httpClient: HttpClient,private data: StudentService, public router: Router, @Inject(MAT_DIALOG_DATA) public data2: any) {
   //this.displayedColumns = [first_name','last_name','email'];
  }

  ngOnInit() {
    this.data.currentMessage.subscribe((message) => this.message = message);
    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
    else{
      console.log(this.message);
      if (("team_members" in this.message)==false){
          console.log("Yes in if")
          var x="[]";
          this.message["team_members"]=x;
          this.data.changeMessage(this.message);
          console.log(this.message);


      }


      this.httpClient.post('http://127.0.0.1:5000/student/regevent', {'student_id': this.message['s_id'], 'e_id': this.message['e_id'], "team_members":this.message["team_members"]}).subscribe(data => {
              this.serverData = data as JSON;
              console.log(this.serverData);
              this.msg= this.serverData["status"]
              console.log(this.msg);
              if((this.msg!="Done")){

                this.msg="Error, you have already registered for this event";
              }

      });


    }
  }

  onClick() {

    this.dialogRef.close();
    this.router.navigateByUrl('/studentprofile');
  }

}
