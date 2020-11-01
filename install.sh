sudo cp raspcuterie.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable raspcuterie.service
sudo systemctl start raspcuterie
