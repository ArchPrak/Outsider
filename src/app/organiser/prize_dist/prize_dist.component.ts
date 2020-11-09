import {Component, Inject} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import {FormsModule} from '@angular/forms';

@Component({
  selector: 'prize-dist',
  templateUrl: 'prize_dist.component.html'
})

export class PrizeDistb {
  prize: string;
  r_id: number;
  message1: string;
  serverData: object;
  constructor(public dialogRef: MatDialogRef<PrizeDistb>, private httpClient: HttpClient, @Inject(MAT_DIALOG_DATA) public data: any) {
  }

  onClick() {
    this.httpClient.post('http://127.0.0.1:5000/allocateprize', {'e_id': this.data.event[0], "r_id": this.r_id, "prize":this.prize}).subscribe(data => {
      this.serverData = data as JSON;
      if(this.serverData["message"] === "successful") {
        this.message1 = "Successful!"

      }
      else {
        this.message1 = "Invalid R_Id for this event";
      }
    }
  )};

  onNoClick() {
    this.dialogRef.close();
  }

  onchange() {
    this.message1 = '';
  }

}

