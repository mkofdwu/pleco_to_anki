# NOTE: because of the way anki dark mode works the blue accent color is in rgb,
# and opacity is separately set

CSS = r'''
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  font-family: 'Avenir LT Std';
}

.card {
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 20px;
  padding: 20px;
}

.chinese {
  font-family: 'Noto Sans';
}

h1 {
  font-weight: 600;
  font-size: 30px;
  margin-bottom: 8px;
}

h2 {
  font-weight: 500;
  font-size: 16px;
  color: #000;
  opacity: 0.6;
  margin-bottom: 44px;
}

.divider {
  width: 100%;
  height: 1px;
  background-color: #000;
  opacity: 0.2;
  margin-bottom: 14px;
}

.type {
  color: #000;
  opacity: 0.2;
  font-size: 12px;
  font-weight: 900;
  text-transform: uppercase;
}

ol {
  list-style-type: none;
  margin-top: 30px;
}

ul {
  list-style-type: disc;
}

ol li {
  display: flex;
  margin-bottom: 16px;
}

.definition-num {
  font-size: 16px;
  font-weight: 800;
  margin-right: 16px;
}

.definition-column {
  font-size: 14px;
}

.definition-column ul {
  margin-top: 14px;
}

.example {
  display: flex;
  color: rgb(90, 115, 180);
  margin-bottom: 14px;
}

.bullet-point {
  width: 6px;
  height: 6px;
  border-radius: 3px;
  background-color: rgb(90, 115, 180);
  margin-top: 8px;
  margin-right: 10px;
}

.example-column {
  display: flex;
  flex-direction: column;
}

.example-column .chinese {
  margin-bottom: 2px;
  font-weight: 500;
}

.example-column .pinyin {
  margin-bottom: 4px;
  font-weight: 500;
  font-size: 12px;
}

.example-column .definition {
  opacity: 0.4;
  font-size: 12px;
}

.very-large {
  font-weight: 600;
  font-size: 64px;
}

.center {
  position: relative;
  text-align: center;
  width: 100%;
  top: 50%;
  transform: translateY(-50%);
}
'''
