<template>
  <div ref="app" id="app">
    <el-card class="card" shadow="always">
      <el-row type="flex" justify="center">
        <el-col>
          <el-steps :active="active" finish-status="success" align-center>
            <el-step title="选取图片"></el-step>
            <el-step title="选择模版"></el-step>
            <el-step title="生成表情包"></el-step>
          </el-steps>
        </el-col>
      </el-row>
      <el-row type="flex" justify="center">
        <el-col>
          <div ref="main" style="margin-top: 20px">
            <el-row type="flex" justify="center">
              <el-col :span="16">
                <el-tabs v-model="activeTab" v-if="active == 1" @tab-click="handleTab">
                  <el-tab-pane name="file" label="上传照片">
                    <photograph
                      v-model="headImage"
                      @upload="upload"
                    ></photograph>
                  </el-tab-pane>
                  <el-tab-pane name="camera" label="手动拍照">
                    <el-row :gutter="10" type="flex" justify="center">
                      <el-col>
                        <video
                          id="videoCamera"
                          :width="videoWidth"
                          :height="videoHeight"
                          autoplay
                        >
                        </video>
                        <canvas
                          style="display: none"
                          id="canvasCamera"
                          :width="videoWidth"
                          :height="videoHeight"
                        ></canvas>
                      </el-col>
                      <el-col>
                        <div>
                          <el-button
                            style="margin-top: 110px"
                            type="success"
                            @click="setImage()"
                            icon="el-icon-camera-solid"
                          ></el-button>
                        </div>
                      </el-col>
                      <el-col>
                        <div class="img_bg_camera">
                          <img :src="imgSrc" alt="" width="videoWidth"
                          height="videoHeight" class="tx_img" />
                        </div>
                      </el-col>
                      <!-- <el-col :span="4">
                        
                      </el-col> -->
                    </el-row>
                  </el-tab-pane>
                </el-tabs>
              </el-col>
            </el-row>
            <el-row
              :gutter="20"
              v-if="active == 2"
              type="flex"
              justify="center"
            >
              <el-col :span="9">
                <el-card>
                  <div slot="header">
                    <span>选择模版</span>
                  </div>
                  <div>
                    <el-table
                      ref="faceTable"
                      :show-header="false"
                      highlight-current-row
                      :data="tableData"
                      :height="250"
                      :max-height="250"
                      style="width: 260px"
                      @row-click="handleSelect"
                    >
                      <el-table-column width="2px" />
                      <el-table-column>
                        <template slot-scope="scope">
                          <el-card>
                            <el-image
                              :src="scope.row.img"
                              style="width: 200px; height: 200px"
                            ></el-image>
                          </el-card>
                        </template>
                      </el-table-column>
                    </el-table>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="9">
                <el-card>
                  <div slot="header">
                    <span>模版描述</span>
                  </div>
                  <div style="height: 250px">
                    <span style="margin-top: 20%">{{ description }}</span>
                  </div>
                </el-card>
              </el-col>
            </el-row>
            <el-row v-if="active == 3" type="flex" justify="center">
              <el-col :span="12">
                <el-image
                  v-loading="loading"
                  element-loading-text="表情包生成中"
                  element-loading-spinner="el-icon-loading"
                  :src="face"
                  :fit="fit"
                  style="width: 400px; height: 400px"
                ></el-image>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
      <el-row type="flex" justify="center" style="margin-top: 10px">
        <el-col :span="3" v-if="active != 3">
          <el-button :disabled="next" type="primary" @click="nextStep"
            >下一步</el-button
          >
        </el-col>
        <el-col :span="3" v-if="active == 2">
          <el-button @click="preStep">上一步</el-button>
        </el-col>
        <el-col v-if="active == 3" :span="6">
          <el-button type="primary" @click="save">保存</el-button>
          <el-button
            type="danger"
            @click="
              () => {
                this.active = 1;
              }
            "
            >重新开始</el-button
          >
        </el-col>
        <!-- <el-col :span="4">
          
        </el-col> -->
      </el-row>
    </el-card>
    <!-- <el-row>
      <el-col>
        
      </el-col>
    </el-row> -->
  </div>
</template>

<script>
import Photograph from "./components/photograph.vue";
import noview from "@/assets/images/noView.jpg";
import { imgsnum, des } from "@/format.js";
import { getStick } from "@/api/axios/msg.js";
import CanvasNest from "canvas-nest.js";

export default {
  name: "app",
  components: {
    Photograph,
  },
  data() {
    return {
      activeTab: "file",
      headImage: "",
      disabled: true,
      next: true,
      tableData: [],
      select: null,
      face: null,
      noView: noview,
      active: 1,
      loading: true,
      description: "",
      videoWidth: 250,
      videoHeight: 300,
      imgSrc: "",
      thisCancas: null,
      thisContext: null,
      thisVideo: null,
    };
  },
  methods: {
    upload() {
      this.next = false;
    },
    handleSelect(row) {
      this.$refs.faceTable.setCurrentRow(row);
      this.disabled = false;
      this.next = false;
      this.select = row.imgIndex;
      this.description = des[row.imgIndex];
    },
    Init() {
      const config = {
        color: "0,0,255",
        count: 200,
      };
      const cn = new CanvasNest(this.$refs["app"], config);
      for (let i = 1; i <= imgsnum; i++) {
        this.tableData.push({
          imgIndex: i,
          img: require("@/assets/images/" + i.toString() + ".jpg"),
        });
      }
    },
    handleTab(tab) {
      if (tab.name == "camera") {
        this.getCompetence();
      } else {
        this.stopNavigator();
      }
    },
    handleFace() {
      //window.alert(this.select);
      this.loading = true;
      let data = new FormData();
      data.append("name", this.select);
      data.append("image", this.headImage);
      getStick(data).then((res) => {
        this.loading = false;
        this.face = window.URL.createObjectURL(res.data);
      });
    },
    nextStep() {
      this.active++;
      this.next = true;
      if (this.active == 2) {
        this.stopNavigator();
      }
      if (this.active == 3) {
        this.handleFace();
      }
      console.log(this.headImage)
    },
    preStep() {
      if (this.active == 2) {
        this.activeTab = "file";
      }
      this.active--;
    },
    save() {
      let a = document.createElement("a");
      a.href = this.face;
      a.download = "stick.jpg";
      a.click();
    },
    getCompetence() {
      var _this = this;
      this.thisCancas = document.getElementById("canvasCamera");
      this.thisContext = this.thisCancas.getContext("2d");
      this.thisVideo = document.getElementById("videoCamera");
      // 旧版本浏览器可能根本不支持mediaDevices，我们首先设置一个空对象
      if (navigator.mediaDevices === undefined) {
        navigator.mediaDevices = {};
      }
      // 一些浏览器实现了部分mediaDevices，我们不能只分配一个对象
      // 使用getUserMedia，因为它会覆盖现有的属性。
      // 这里，如果缺少getUserMedia属性，就添加它。
      if (navigator.mediaDevices.getUserMedia === undefined) {
        navigator.mediaDevices.getUserMedia = function (constraints) {
          // 首先获取现存的getUserMedia(如果存在)
          var getUserMedia =
            navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia ||
            navigator.getUserMedia;
          // 有些浏览器不支持，会返回错误信息
          // 保持接口一致
          if (!getUserMedia) {
            return Promise.reject(
              new Error("getUserMedia is not implemented in this browser")
            );
          }
          // 否则，使用Promise将调用包装到旧的navigator.getUserMedia
          return new Promise(function (resolve, reject) {
            getUserMedia.call(navigator, constraints, resolve, reject);
          });
        };
      }
      var constraints = {
        audio: false,
        video: {
          width: this.videoWidth,
          height: this.videoHeight,
          transform: "scaleX(-1)",
        },
      };
      navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function (stream) {
          // 旧的浏览器可能没有srcObject
          if ("srcObject" in _this.thisVideo) {
            _this.thisVideo.srcObject = stream;
          } else {
            // 避免在新的浏览器中使用它，因为它正在被弃用。
            _this.thisVideo.src = window.URL.createObjectURL(stream);
          }
          _this.thisVideo.onloadedmetadata = function (e) {
            _this.thisVideo.play();
          };
        })
        .catch((err) => {
          console.log(err);
        });
    },
    //  绘制图片（拍照功能）

    setImage() {
      var _this = this;
      // 点击，canvas画图
      _this.thisContext.drawImage(
        _this.thisVideo,
        0,
        0,
        _this.videoWidth,
        _this.videoHeight
      );
      this.thisCancas.toBlob(b=>{this.headImage=b},"image/jpeg");
      let image = this.thisCancas.toDataURL("image/jpeg")
      _this.imgSrc = image
      //_this.headImage = image
      _this.next = false;
    },
    // base64转文件

    dataURLtoFile(dataurl, filename) {
      var arr = dataurl.split(",");
      var mime = arr[0].match(/:(.*?);/)[1];
      var bstr = atob(arr[1]);
      var n = bstr.length;
      var u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], filename, { type: mime });
    },
    // 关闭摄像头
    stopNavigator() {
      this.thisVideo.srcObject.getTracks()[0].stop();
    },
  },
  mounted() {
    this.Init();
  },
};
</script>

<style>
html,
body {
  position: fixed;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}
#app {
  position: fixed;
  margin: 0;
  height: 100%;
  width: 100%;
}
.el-table--striped .el-table__body tr.el-table__row--striped.current-row td,
.el-table__body tr.current-row > td {
  color: #fff;
  background-color: blue !important;
}
.card {
  margin-top: 10%;
  margin-left: 20%;
  margin-right: 20%;
  margin-bottom: 10%;
  color: black;
}
</style>
