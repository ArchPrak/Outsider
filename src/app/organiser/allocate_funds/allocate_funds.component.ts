import {Component, Inject} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { OrganiserService } from 'src/app/organiser.service';

@Component({
  selector: 'fund-allocate-form',
  templateUrl: 'allocate_funds.component.html',
})

export class DialogOverviewExampleDialog {
  amount:number;
  reason: string;
  message:object;
  serverData: JSON;
  message1: string;
  message2: string;
  constructor(private data1: OrganiserService, public dialogRef: MatDialogRef<DialogOverviewExampleDialog>, private httpClient: HttpClient, @Inject(MAT_DIALOG_DATA) public data: any) {
  }

  ngOnInit() {
    this.data1.currentMessage.subscribe((message) => this.message = message);
    console.log(this.data1.currentMessage);
  }

  onClick() {
    console.log(this.amount);
    console.log(this.reason);
    console.log(this.data);
    if(this.amount && this.reason) {
      this.httpClient.post('http://127.0.0.1:5000/allocatefunds', {'o_id': this.message['o_id'], 'e_id': this.data.event[0], "amount": this.amount, "reason": this.reason}).subscribe(data => {
        this.serverData = data as JSON;
        console.log(this.serverData);
        this.message1 = this.serverData["message"]
        console.log(this.message1);
        if(this.message1 === "successful") {
          this.closeDialog();
        }
        else {
          this.message1 = "Insufficient funds!"
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
