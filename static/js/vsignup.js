function vol-pref-drop-select {
  document.getElementById('displayValue').value=this.options[this.selectedIndex].text;
  document.getElementById('idValue').value=this.options[this.selectedIndex].value;
}