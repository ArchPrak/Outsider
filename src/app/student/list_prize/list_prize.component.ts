import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';




@Component({
  selector: 'all-prize',
  templateUrl: './list_prize.component.html'
})

export class DispPrizes{
  message: object;
  serverData: object;
  info:object;

  constructor(private httpClient: HttpClient, private data: StudentService, public router: Router) {

  }
  headers=["Event name","Prize"];

  ngOnInit() {
    this.data.currentMessage.subscribe((message) => this.message = message);
    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
    else {
      this.httpClient.post('http://127.0.0.1:5000/student/prizes', {'student_id': this.message['s_id']}).subscribe(data => {
        this.serverData = data as JSON;
        console.log(this.serverData);
      });
      this.httpClient.post('http://127.0.0.1:5000/student/info', {'student_id': this.message['s_id']}).subscribe(data => {
        this.info = data as JSON;
        console.log(this.info);
      });
    };
  }


}
