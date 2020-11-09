import {Component, Inject} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import {MatTableModule} from '@angular/material/table';

import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';
import { ArrayDataSource } from '@angular/cdk/collections';

@Component({
  selector: 'team_input',
  templateUrl: 'team_input.component.html',
})

export class TeamInput {

  team_mem: string;
  mem:string;
  message:object;
  serverData: object;

  serverData2: JSON;
  message1: string;
  message2: string;
  constructor(private data1: StudentService, public dialogRef: MatDialogRef<TeamInput>, private httpClient: HttpClient, @Inject(MAT_DIALOG_DATA) public data: any) {
  }

  ngOnInit() {
    this.data1.currentMessage.subscribe((message) => this.message = message);
    console.log(this.data1.currentMessage);
  }

  onClick() {
    console.log(this.team_mem);
    console.log(this.data);
    if(this.team_mem) {
      console.log(this.team_mem);
      this.mem="["+this.team_mem+ "]";
      this.httpClient.post('http://127.0.0.1:5000/student/regchk', {'student_id': this.message['s_id'], 'e_id': this.message['e_id'], "team":this.mem}).subscribe(data => {
        this.serverData = data as JSON;
        console.log(this.serverData);
        this.message1 = this.serverData["message"]
        console.log(this.message1);
        if(this.message1 == "successful") {

        this.message["team_members"]=this.mem;
        this.data1.changeMessage(this.message);
        this.message1="Success!"
        this.message2="Please proceed to payment";
              //call next api to reg event
          //this.closeDialog();
        }
        else {
          this.message2 =this.message1;
          this.message1="Error!";
        }
      });
    }
    else{
      this.message2 = "Enter all details!";
    }
  }

  mess2() {
    this.message2 = ""
    this.message1 = ""
  }

  closeDialog() {
    this.dialogRef.close();
  }

  onNoClick() {
    this.dialogRef.close();
  }
}
