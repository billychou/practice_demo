/**
 * Created by songchuanzhou on 17/1/7.
 */

import { Component } from '@angular/core';

@Component({
  selector: 'click-me',
  templateUrl: "b.html"
})


export class ClickMeComponent {
  clickMessage = '';
  onClickMe() {
    this.clickMessage = "you are my hero";
  }


}


