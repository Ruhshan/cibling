self.addEventListener('message',(ev)=>{

    self.postMessage(ev.data)
})