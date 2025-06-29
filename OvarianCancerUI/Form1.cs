using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using BackLayer;

namespace OvarianCancer
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        string selectedPath;

        private void button2_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog ofd = new OpenFileDialog())
            {
                ofd.Title = "Select an Image";
                ofd.Filter = "Image Files (*.png;*.jpg;*.jpeg;*.bmp)|*.png;*.jpg;*.jpeg;*.bmp";

                if (ofd.ShowDialog() == DialogResult.OK)
                {
                     selectedPath = ofd.FileName;
                    pictureBox1.Image = Image.FromFile(selectedPath);
                    pictureBox1.SizeMode = PictureBoxSizeMode.Zoom;
                }
            }
        }

        private async void button1_Click(object sender, EventArgs e)
        {
            var predictor = new BackLayer.ImagePredictor(); // assuming it's in namespace BackLayer
            try
            {
                var result = await predictor.PredictImageAsync(selectedPath);
                lbCancerType.Text = result.Class;
                lbConfidenceRate.Text=result.Confidence.ToString();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "Prediction Failed");
            }

        }
    }
}