import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, Routes, RouterModule } from '@angular/router';
import { OrganiserService } from '../../organiser.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogOverviewExampleDialog } from '../allocate_funds/allocate_funds.component';
import { ExpenseLog } from '../expense_log/expense_log.component';
import { PrizeDistb } from '../prize_dist/prize_dist.component';
import { DisplayRegistrationTable } from '../display_reg/display_reg.component';
import {CommonModule} from '@angular/common';
import { splitAtColon } from '@angular/compiler/src/util';

@Component({
  selector: 'all-event',
  templateUrl: './list_event.component.html',
  styleUrls: ['list_event.component.css', '../../../../node_modules/materialize-css/dist/css/materialize.min.css', '../../../../node_modules/bootstrap/dist/css/bootstrap.min.css']
})

export class AllEvents {
  message: object;
  serverData: object;
  serverData1: object;
  serverDataPast: Array<object>;
  serverDataPresent: Array<object>;
  amount: number;
  event: object;
  rem_fund: object;
  constructor(private httpClient: HttpClient, private data: OrganiserService, public router: Router, public dialog: MatDialog) {

  }

  ngOnInit() {
    this.data.currentMessage.subscribe((message) => this.message = message);
    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
    else {
      this.random();
    }
  }

  async random() {
    await this.httpClient.post('http://127.0.0.1:5000/listevents', {'o_id': this.message['o_id']}).toPromise().then(data => {
        this.serverData = data as JSON;
        console.log(this.serverData);
        var e_ids = []
        for(var x in this.serverData) {
          console.log(this.serverData[x][0]);
          e_ids.push(this.serverData[x][0]);
        }
        console.log(e_ids);
        var funds_rem = []
        var i = 0;
        this.random2(e_ids);
      });
    }

  async random2(e_ids) {
    var i = 0;
    for(var x in e_ids) {
      await this.httpClient.post('http://127.0.0.1:5000/fund_rem', {'e_id': e_ids[x]}).toPromise().then(data => {
        this.serverData1 = data as JSON;
        console.log(this.serverData1);
        this.serverData[i++].push(this.serverData1["rem_funds"]);
        this.split();
      });
  }
}
  split() {
    var date = new Date();
    var i = 0, j = 0;
    this.serverDataPast = []
    this.serverDataPresent = []
    for(var x in this.serverData) {
      var split_date = this.serverData[x][5].split('-');
      var d1 = new Date(Number(split_date[0]), Number(split_date[1]) - 1, Number(split_date[2]));
      console.log(d1);
      if(d1 > date) {
        this.serverDataPresent.push({});
        this.serverDataPresent[i++] = (this.serverData[x]);
      }
      else {
        this.serverDataPast.push({})
        this.serverDataPast[j++] = this.serverData[x];
      }
    }
    console.log(this.serverDataPresent);
    console.log(this.serverDataPast);
  }

  fund(event) {
    this.event = event;
    const dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      width: '300px',
      data: {event: this.event}
    })
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.ngOnInit();
    });
  }

  expense_log(event) {
    this.event = event;
    const dialogRef = this.dialog.open(ExpenseLog, {
      width: '300px',
      data: {event: this.event}
    })
  }

  give_prize(event) {
    this.event = event;
    const dialogRef = this.dialog.open(PrizeDistb, {
      width: '300px',
      data: {event: this.event}
    });
  }

  see_registrations(event) {
    this.event = event;
    const dialogRef = this.dialog.open(DisplayRegistrationTable, {
      width: '600px',
      data: {event: this.event}
    })
    this.httpClient.post('http://127.0.0.1:5000/show_reg', {'e_id': this.event[0]}).subscribe(data => {
      console.log(data);
    })


  }

  complete_event(event) {
    this.event = event;
    this.httpClient.post('http://127.0.0.1:5000/event_comp', {'e_id': this.event[0]}).subscribe(data => {
      console.log(data);
    })
  }
}

