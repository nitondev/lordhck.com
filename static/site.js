const b=new Date(1994,10,2),t=new Date();
const age=t.getFullYear()-b.getFullYear()-(t<b.setFullYear(t.getFullYear()));
document.getElementById("age").textContent=age;
