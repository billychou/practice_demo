/**
 * Created by songchuanzhou on 17/1/5.
 */

import { Component } from '@angular/core';


@Component({
  selector: 'ctor',
  templateUrl: "ctor.html"
})


export class AppCtorComponent {
  title: string;
  myHero: string;

  constructor() {
    this.title = "Tour of Heroes";
    this.myHero = "Windstorm";
  }

}
