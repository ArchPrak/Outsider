import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';
import { FormGroup, FormControl, ReactiveFormsModule, EmailValidator } from '@angular/forms';

@Component({
  selector: 'hobby',
  templateUrl: './add_hobby.component.html'
})

export class AddHobby {
  message: object;
  serverData: object;
  hobbyForm: FormGroup;

  constructor(private httpClient: HttpClient, private data: StudentService, public router: Router) {
    this.hobbyForm = new FormGroup({
      hobby: new FormControl(''),
    });
  }
  add_hobby() {
    this.data.currentMessage.subscribe((message) => this.message = message);
    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
    else {
      this.httpClient.post('http://127.0.0.1:5000/student/hobby', {'student_id': this.message['s_id'],'hobby':this.hobbyForm.value["hobby"]}).subscribe(data => {
        this.serverData = data as JSON;
        console.log(this.serverData);
      });
    };
  }
}

