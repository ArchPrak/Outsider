import {Component, Inject} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import {FormsModule} from '@angular/forms';
import {Router} from '@angular/router';
import {MatButtonModule} from '@angular/material/button';

@Component({
  selector: 'disp-hobby',
  templateUrl: 'disp_hobby.component.html'
})

export class DispHobby {
  message1: string;
  serverData: object;
  constructor(public dialogRef: MatDialogRef<DispHobby>, private httpClient: HttpClient, @Inject(MAT_DIALOG_DATA) public data: any, public router: Router) {
  }
  onNoClick() {
    this.dialogRef.close();
  }

  add_hobby() {
    console.log(this.data.interests)
  this.httpClient.post('http://127.0.0.1:5000/student/hobby', {'s_id': this.data.id,'hobby':this.data.interests}).subscribe(data => {
        this.serverData = data as JSON;
        console.log(this.serverData);
        this.dialogRef.close();
        this.router.navigateByUrl('/studentprofile');
      });

  }
}
