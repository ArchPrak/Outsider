import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';




@Component({
  selector: 'get-team',
  templateUrl: './get_team.component.html'
})

export class GetTeam{
  message: object;
  serverData: object;
  displayedColumns: object;
  constructor(private httpClient: HttpClient, private data: StudentService, public router: Router) {
    this.displayedColumns = ["Name", "Email"]
  }


  ngOnInit() {
    this.data.currentMessage.subscribe((message) => this.message = message);
    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
    else {
      this.httpClient.post('http://127.0.0.1:5000/student/team', {'student_id': this.message['s_id']}).subscribe(data => {
        this.serverData = data as JSON;

        console.log(this.serverData);
      });
    };
  }


}
