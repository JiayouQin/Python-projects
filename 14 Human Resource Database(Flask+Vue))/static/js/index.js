const app = Vue.createApp({

    delimiters : ['[[', ']]'],
    data() {
        return {
            edit_mode: false,
            engineers: [{id: 0, name: '张三', province: '上海', major: '一级建筑师', cell: '123456',registered:'否',previous_unit:'无',QQ:'541654',note:'张三天天打麻将'},
                        {id: 1, name: '李四', province: '北京', major: '德语翻译', cell: '123456',registered:'否',previous_unit:'无'}],
        }
    },
  methods: {
    toggle_edit(){
      console.log('edit_mode: '+this.edit_mode)
      this.edit_mode = !this.edit_mode
    },
    del_entry(id,index){
      console.log(id,index)
      var xhr = new XMLHttpRequest();
      xhr.open("POST", '', true);
      xhr.setRequestHeader("Content-Type", "application/json");
      var data = JSON.stringify({'delete':true,'id':id});
      xhr.send(data);
      this.engineers.splice(index,1)

    },
    upload(id,i){
      let name = this.engineers[i].name
      let province = this.engineers[i].province
      let major = this.engineers[i].major
      let cell = this.engineers[i].cell
      let registered = this.engineers[i].registered
      let phone = this.engineers[i].phone
      let qq = this.engineers[i].qq
      let wechat = this.engineers[i].wechat
      let registered_unit = this.engineers[i].registered_unit
      let previous_unit = this.engineers[i].previous_unit
      let note = this.engineers[i].note

      console.log(id,name,province,major,cell,registered,phone)

      params={'id':id,'name':name,'province':province,'major':major,'cell':cell,'registered':registered,'phone':phone,'qq':qq,'wechat':wechat,
      'registered_unit':registered_unit,'previous_unit':previous_unit,'note':note}

      var xhr = new XMLHttpRequest();
      xhr.open("POST", '', true);
      xhr.setRequestHeader("Content-Type", "application/json");
      var data = JSON.stringify(params);
      xhr.send(data);
      alert("已发送修改请求");
      //window.location.reload();
    },
    create_entry(){
      let name = document.getElementsByName('name')[0].value
      let province = document.getElementsByName('province')[0].value
      let major = document.getElementsByName('major')[0].value
      let cell = document.getElementsByName('cell')[0].value
      let qq = document.getElementsByName('qq')[0].value
      let wechat = document.getElementsByName('wechat')[0].value
      let note = document.getElementsByName('note')[0].value
      let registered = document.getElementsByName('registered')[0].selectedIndex
      console.log(name,province,major,cell,qq,wechat,note,registered)

      params={'id':null,'name':name,'province':province,'major':major,'cell':cell,'registered':registered,'qq':qq,'wechat':wechat,'note':note,'new':true}

      var xhr = new XMLHttpRequest();
      xhr.open("POST", '', true);
      xhr.setRequestHeader("Content-Type", "application/json");
      var data = JSON.stringify(params);
      xhr.send(data);
      window.location.reload()
    },
  }
})


