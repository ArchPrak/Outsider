import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, Routes, RouterModule } from '@angular/router';
import { OrganiserService } from '../../organiser.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogOverviewExampleDialog } from '../allocate_funds/allocate_funds.component';


@Component({
  selector: 'all-event',
  templateUrl: './list_event.component.html'
})

export class AllEvents {
  message: object;
  serverData: object;
  amount: number;
  constructor(private httpClient: HttpClient, private data: OrganiserService, public router: Router, public dialog: MatDialog) {

  }

  ngOnInit() {
    this.data.currentMessage.subscribe((message) => this.message = message);
    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
    else {
      this.httpClient.post('http://127.0.0.1:5000/listevents', {'o_id': this.message['o_id']}).subscribe(data => {
        this.serverData = data as JSON;
        console.log(this.serverData);
      });
    };
  }

  fund(event) {
    const dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      width: '250px',
      data: {name: this.amount}
    })

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.amount = result;
      console.log(this.amount + "here");
    });

  }

}
