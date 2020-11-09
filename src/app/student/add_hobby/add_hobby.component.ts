import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';
import { FormGroup, FormControl, ReactiveFormsModule, EmailValidator } from '@angular/forms';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatFormFieldModule} from '@angular/material/form-field';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';

import {DispHobby} from '../disp_hobby/disp_hobby.component';
@Component({
  selector: 'hobby',
  templateUrl: './add_hobby.component.html'
})

export class AddHobby {
  message: object;
  serverData: object;
  interests = []; cChecked; mChecked; sChecked;pChecked; dChecked; aChecked;wChecked;
  id: number;


  constructor(private httpClient: HttpClient, private data: StudentService, public router: Router,public dialog: MatDialog) {

  }
  ngOnInit() {
    this.data.currentMessage.subscribe((message) => this.message = message);

  }

  onCheckboxChagen(event, value) {

    if (event.checked) {

      this.interests.push(value);
    }

    if (!event.checked) {

      let index = this.interests.indexOf(value);
      if (index > -1) {
        this.interests.splice(index, 1);
      }
    }

    console.log("Interests array => " + JSON.stringify(this.interests, null, 2));
  }


  disp_hobby()
  {
    console.log(this.message);
    this.id = this.message['s_id'];

    console.log(this.id);
    const dialogRef = this.dialog.open(DispHobby, {
      width: '300px',
       data: {interests: this.interests, id: this.id}
    });
  }

}
